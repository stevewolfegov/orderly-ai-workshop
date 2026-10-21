# Orderly pricing rules

Owner: Product team. Last reviewed: 2026-03-02.

These rules are the source of truth for how Orderly prices an order. If the code
disagrees with this document, the code is wrong.

## Line items

- Each order has 1 to 50 line items.
- Each line's quantity is a whole number from 1 to 100.
- A line's total is the unit price multiplied by the quantity.
- **Bulk discount:** a line with a quantity of 10 or more gets 10% off that line.
  The bulk discount applies per line, not across the whole order.

The **subtotal** is the sum of the line totals after bulk discounts.

## Automatic discounts

Automatic discounts are calculated from the subtotal.

| Rule | Discount |
| --- | --- |
| Gold tier customer | 5% off |
| Platinum tier customer | 10% off |
| Subtotal of $500.00 or more | An extra 5% off |

Platinum customers don't receive the $500 order-size discount, because their tier
discount already covers it. Gold customers receive both.

## Promo codes

- An order can use one promo code. Codes aren't case-sensitive.
- A code must be active and not expired, and the subtotal must meet the code's
  minimum.
- Promo code types:
  - `percent`: a percentage off the subtotal **after** automatic discounts.
  - `fixed`: a fixed dollar amount off. The total discount can't exceed the
    subtotal.
  - `freeship`: free shipping. No price discount.

The **discounted subtotal** is the subtotal minus all discounts.

## Shipping

- Flat rate: $7.99.
- Free when the **discounted subtotal** is $75.00 or more.
- Always free for platinum customers.
- Free with a `freeship` promo code.

## Sales tax

Tax applies to the discounted subtotal. Shipping isn't taxed.

| State | Rate |
| --- | --- |
| CA | 7.25% |
| NY | 4.00% |
| TX | 6.25% |
| WA | 6.50% |
| Any other state | 5.00% |

## Totals

Total = discounted subtotal + shipping + tax.

Round each reported amount to the nearest cent.

## Invoices

An invoice must show exactly the amounts that were charged when the order was
placed. Invoices never recalculate prices.
