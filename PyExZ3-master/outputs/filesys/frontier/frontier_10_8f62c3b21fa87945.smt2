(set-logic ALL)
; Frontier Constraint ID: 8f62c3b21fa87945
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1327)) (False)
(assert (not (not (= x 1327))))

(check-sat)
(get-model)
