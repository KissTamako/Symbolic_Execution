(set-logic ALL)
; Frontier Constraint ID: eb55445676aef151
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1477)) (False)
(assert (not (not (= x 1477))))

(check-sat)
(get-model)
