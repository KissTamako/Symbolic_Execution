(set-logic ALL)
; Frontier Constraint ID: 9b1e9252d250372b
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1030)) (False)
(assert (not (= x 1030)))

; Query: ((== x 1031)) (False)
(assert (not (not (= x 1031))))

(check-sat)
(get-model)
