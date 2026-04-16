(set-logic ALL)
; Frontier Constraint ID: bf2bd57ec61cebe0
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1321)) (False)
(assert (not (not (= x 1321))))

(check-sat)
(get-model)
