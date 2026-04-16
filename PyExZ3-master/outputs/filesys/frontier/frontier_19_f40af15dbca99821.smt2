(set-logic ALL)
; Frontier Constraint ID: f40af15dbca99821
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1714)) (False)
(assert (not (= x 1714)))

; Query: ((== x 1715)) (False)
(assert (not (not (= x 1715))))

(check-sat)
(get-model)
