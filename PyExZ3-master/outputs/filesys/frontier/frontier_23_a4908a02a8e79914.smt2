(set-logic ALL)
; Frontier Constraint ID: a4908a02a8e79914
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1045)) (False)
(assert (not (= x 1045)))

; Query: ((== x 1046)) (False)
(assert (not (not (= x 1046))))

(check-sat)
(get-model)
