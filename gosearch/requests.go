package main

import (
	"context"
	"time"
	"log"

	"github.com/chromedp/cdproto/network"
	"github.com/chromedp/chromedp"
)

type ContextHandle struct {
	Ctx context.Context
	Cancel context.CancelFunc
}

type Browser struct {
	AllocCtx ContextHandle
	BrowserCtx ContextHandle
}

func NewBrowser() (*Browser, error) {
	allocCtx, allocCancel := chromedp.NewExecAllocator(
		context.Background(),
		append(chromedp.DefaultExecAllocatorOptions[:],
			chromedp.Flag("headless", true),
			chromedp.UserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"),
		)...,
	)

	browserCtx, browserCancel := chromedp.NewContext(allocCtx, chromedp.WithDebugf(log.Printf))
	err := chromedp.Run(browserCtx)
	if err != nil {
		browserCancel()
		allocCancel()
		return nil, err
	}

	return &Browser{
		ContextHandle{allocCtx, allocCancel},
		ContextHandle{browserCtx, browserCancel},
	}, nil
}

func GetRendered(browser *Browser, url string) (string, string, int, error) {
	ctx, cancel := chromedp.NewContext(browser.BrowserCtx.Ctx)
	defer cancel()

	ctx, timeoutCancel := context.WithTimeout(ctx, 20*time.Second)
	defer timeoutCancel()

	var renderedHtml, text string
	var resCode int

	if err := chromedp.Run(ctx, network.Enable()); err != nil {
		return "", "", 0, err
	}

	chromedp.ListenTarget(ctx, func(e interface{}) {
		// Get event as proper type
		res, ok := e.(*network.EventResponseReceived)

		// Check code
		if ok && res.Type == network.ResourceTypeDocument {
			resCode = int(res.Response.Status)
		}
	})

	// Navigate and extract
	err := chromedp.Run(ctx,
		chromedp.Navigate(url),
		chromedp.Evaluate(`document.readyState`, &readyState),
		chromedp.WaitFunc(func(ctx context.Context) error {
			var ready string
			if err := chromedp.Evaluate(`document.readyState`, &ready).Do(ctx); err != nil {
				return err
			}
			if ready != "complete" {
				return errors.New("page not ready")
			}
			return nil
		}),
		chromedp.OuterHTML("renderedHtml", &renderedHtml),
		chromedp.Text("body", &text),
	)

	if err != nil {
		return "", "", 0, err
	}

	return renderedHtml, text, resCode, nil
}

func ResponseOk(resCode int) bool {
	return resCode / 100 == 2
}
