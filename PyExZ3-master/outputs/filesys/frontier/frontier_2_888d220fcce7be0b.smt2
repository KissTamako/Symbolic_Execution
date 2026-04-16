(set-logic ALL)
; Frontier Constraint ID: 888d220fcce7be0b
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 340)) (False)
(assert (not (not (= x 340))))

(check-sat)
(get-model)
