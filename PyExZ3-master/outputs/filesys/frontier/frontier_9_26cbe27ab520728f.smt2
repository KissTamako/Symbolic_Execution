(set-logic ALL)
; Frontier Constraint ID: 26cbe27ab520728f
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 499)) (False)
(assert (not (= x 499)))

; Query: ((== x 500)) (False)
(assert (not (not (= x 500))))

(check-sat)
(get-model)
