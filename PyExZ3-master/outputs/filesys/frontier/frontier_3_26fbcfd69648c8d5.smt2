(set-logic ALL)
; Frontier Constraint ID: 26fbcfd69648c8d5
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 715)) (False)
(assert (not (= x 715)))

; Query: ((== x 716)) (False)
(assert (not (not (= x 716))))

(check-sat)
(get-model)
