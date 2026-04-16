(set-logic ALL)
; Frontier Constraint ID: f5fb2bbbb828c426
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 502)) (False)
(assert (not (= x 502)))

; Query: ((== x 503)) (False)
(assert (not (not (= x 503))))

(check-sat)
(get-model)
