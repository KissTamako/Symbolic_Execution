(set-logic ALL)
; Frontier Constraint ID: 009243785bf05f35
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 520)) (False)
(assert (not (not (= x 520))))

(check-sat)
(get-model)
