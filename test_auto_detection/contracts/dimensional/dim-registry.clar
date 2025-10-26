;; Dimensional Registry contract for auto-detection test
(define-map dimensions
  { id: uint }
  { name: (string-ascii 64) })

(define-public (register-dimension (id uint) (name (string-ascii 64)))
  (ok true))
