;; DEX Factory contract for auto-detection test
(define-map pools
  { token-x: principal, token-y: principal }
  { pair: principal })

(define-public (create-pair (token-x principal) (token-y principal))
  (ok true))
