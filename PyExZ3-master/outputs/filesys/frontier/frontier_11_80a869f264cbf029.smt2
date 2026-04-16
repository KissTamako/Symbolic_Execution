(set-logic ALL)
; Frontier Constraint ID: 80a869f264cbf029
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1477)) (False)
(assert (not (= x 1477)))

; Query: ((== x 1478)) (False)
(assert (not (not (= x 1478))))

(check-sat)
(get-model)
