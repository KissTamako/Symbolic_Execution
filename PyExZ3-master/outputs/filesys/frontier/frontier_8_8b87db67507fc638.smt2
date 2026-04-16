(set-logic ALL)
; Frontier Constraint ID: 8b87db67507fc638
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1324)) (False)
(assert (not (not (= x 1324))))

(check-sat)
(get-model)
