import { expect, test } from "@playwright/test";

test("has title", async ({ page }) => {
  await page.goto("/");
  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Outputudy/);
});

test("redirects to login when unauthenticated", async ({ page }) => {
  await page.goto("/dashboard");
  await expect(page).toHaveURL(/.*\/login/);
});
