(set-logic ALL)
; Frontier Constraint ID: 005340fc3b782457
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 880)) (False)
(assert (not (= x 880)))

; Query: ((== x 881)) (False)
(assert (not (not (= x 881))))

(check-sat)
(get-model)
