;; DLC Bond Contract
;; Handles collateralized bonds using DLCs.
;; Copyright (c) 2025 Conxian-Labs. This software is released under the MIT License.

(define-constant ERR_INSUFFICIENT_COLLATERAL (err u402))

(define-map bonds
    { bond-id: uint }
    {
        owner: principal,
        amount: uint,
        collateral-ratio: uint,
        active: bool
    }
)

(define-public (issue-bond (bond-id uint) (amount uint) (ratio uint))
    (begin
        (map-set bonds
            { bond-id: bond-id }
            {
                owner: tx-sender,
                amount: amount,
                collateral-ratio: ratio,
                active: true
            }
        )
        (ok bond-id)
    )
)

(define-read-only (get-bond (bond-id uint))
    (map-get? bonds { bond-id: bond-id })
)
