(set-logic ALL)
; Frontier Constraint ID: 6c5127299563714c
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 580)) (False)
(assert (not (not (= x 580))))

(check-sat)
(get-model)
