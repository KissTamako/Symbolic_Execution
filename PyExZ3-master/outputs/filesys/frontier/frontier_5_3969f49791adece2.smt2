(set-logic ALL)
; Frontier Constraint ID: 3969f49791adece2
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 868)) (False)
(assert (not (= x 868)))

; Query: ((== x 869)) (False)
(assert (not (not (= x 869))))

(check-sat)
(get-model)
