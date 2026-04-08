;; Revenue Automation Contract
;; Responsible for non-negotiable 100 bps (1%) protocol fee extraction.
;; Copyright (c) 2026 Conxian-Labs. This software is released under the MIT License.

(use-trait sip-010-ft-trait .sip-010-ft-trait.sip-010-ft-trait)

(define-constant ERR_UNAUTHORIZED (err u401))
(define-constant ERR_INVALID_AMOUNT (err u400))
(define-constant ERR_TRANSFER_FAILED (err u402))

(define-data-var contract-admin principal tx-sender)
(define-data-var protocol-wallet principal tx-sender)
(define-data-var fee-bps uint u100) ;; 100 BPS = 1% Sovereign Tax

(define-read-only (is-admin)
    (is-eq tx-sender (var-get contract-admin))
)

;; @desc Calculate and extract fee natively in STX
;; @param amount The gross amount
;; @param recipient The final recipient of the net amount
;; @returns (response { fee: uint, net: uint } uint)
(define-public (process-revenue-stx (amount uint) (recipient principal))
    (let (
        (fee (/ (* amount (var-get fee-bps)) u10000))
        (net-amount (- amount fee))
    )
    (begin
        (asserts! (> amount u0) ERR_INVALID_AMOUNT)
        ;; Transfer fee to protocol treasury
        (unwrap! (stx-transfer? fee tx-sender (var-get protocol-wallet)) ERR_TRANSFER_FAILED)
        ;; Transfer net to recipient
        (unwrap! (stx-transfer? net-amount tx-sender recipient) ERR_TRANSFER_FAILED)
        (ok { fee: fee, net: net-amount })
    ))
)

;; @desc Calculate and extract fee for SIP-010 tokens
;; @param amount The gross amount
;; @param recipient The final recipient of the net amount
;; @param token The SIP-010 token trait
;; @returns (response { fee: uint, net: uint } uint)
(define-public (process-revenue-sip010 (amount uint) (recipient principal) (token <sip-010-ft-trait>))
    (let (
        (fee (/ (* amount (var-get fee-bps)) u10000))
        (net-amount (- amount fee))
    )
    (begin
        (asserts! (> amount u0) ERR_INVALID_AMOUNT)
        ;; Transfer fee to protocol treasury
        (unwrap! (contract-call? token transfer fee tx-sender (var-get protocol-wallet) none) ERR_TRANSFER_FAILED)
        ;; Transfer net to recipient
        (unwrap! (contract-call? token transfer net-amount tx-sender recipient none) ERR_TRANSFER_FAILED)
        (ok { fee: fee, net: net-amount })
    ))
)

;; @desc Update the protocol wallet (Admin only)
(define-public (set-protocol-wallet (new-wallet principal))
    (begin
        (asserts! (is-admin) ERR_UNAUTHORIZED)
        (var-set protocol-wallet new-wallet)
        (ok true)
    )
)

;; @desc Update contract admin (Admin only)
(define-public (set-contract-admin (new-admin principal))
    (begin
        (asserts! (is-admin) ERR_UNAUTHORIZED)
        (var-set contract-admin new-admin)
        (ok true)
    )
)

(define-read-only (get-contract-admin)
    (ok (var-get contract-admin))
)

(define-read-only (get-fee-bps)
    (ok (var-get fee-bps))
)
