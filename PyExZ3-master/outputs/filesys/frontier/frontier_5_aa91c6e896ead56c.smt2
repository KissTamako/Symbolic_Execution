(set-logic ALL)
; Frontier Constraint ID: aa91c6e896ead56c
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2443)) (False)
(assert (not (= x 2443)))

; Query: ((== x 2444)) (False)
(assert (not (not (= x 2444))))

(check-sat)
(get-model)
