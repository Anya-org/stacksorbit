;; DLC Orchestrator Contract
;; Manages Discrete Log Contracts lifecycle on Stacks.
;; Copyright (c) 2025 Anya Chain Labs. This software is released under the MIT License.

(define-map dlc-contracts
    { dlc-id: (buff 32) }
    {
        oracle: principal,
        collateral: uint,
        status: (string-ascii 20),
        expiry: uint
    }
)

(define-public (open-dlc (dlc-id (buff 32)) (oracle principal) (collateral uint) (expiry uint))
    (begin
        (map-set dlc-contracts
            { dlc-id: dlc-id }
            {
                oracle: oracle,
                collateral: collateral,
                status: "OPEN",
                expiry: expiry
            }
        )
        (ok true)
    )
)

(define-read-only (get-dlc-status (dlc-id (buff 32)))
    (map-get? dlc-contracts { dlc-id: dlc-id })
)
