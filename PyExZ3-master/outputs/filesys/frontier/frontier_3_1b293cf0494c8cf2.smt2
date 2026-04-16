(set-logic ALL)
; Frontier Constraint ID: 1b293cf0494c8cf2
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 340)) (False)
(assert (not (= x 340)))

; Query: ((== x 341)) (False)
(assert (not (not (= x 341))))

(check-sat)
(get-model)
