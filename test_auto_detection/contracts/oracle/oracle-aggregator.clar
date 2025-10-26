;; Oracle Aggregator contract for auto-detection test
(define-map price-feeds
  { asset: (string-ascii 32) }
  { price: uint, timestamp: uint })

(define-public (get-price (asset (string-ascii 32)))
  (ok u1000))
