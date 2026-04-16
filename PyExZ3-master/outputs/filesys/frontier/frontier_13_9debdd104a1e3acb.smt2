(set-logic ALL)
; Frontier Constraint ID: 9debdd104a1e3acb
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1180)) (False)
(assert (not (= x 1180)))

; Query: ((== x 1181)) (False)
(assert (not (not (= x 1181))))

(check-sat)
(get-model)
