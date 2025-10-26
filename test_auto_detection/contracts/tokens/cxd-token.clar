;; CXD Token contract for auto-detection test
(define-fungible-token cxd-token)

(define-public (mint (amount uint))
  (ok amount))
