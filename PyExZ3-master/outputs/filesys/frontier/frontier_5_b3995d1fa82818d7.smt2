(set-logic ALL)
; Frontier Constraint ID: b3995d1fa82818d7
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2818)) (False)
(assert (not (= x 2818)))

; Query: ((== x 2819)) (False)
(assert (not (not (= x 2819))))

(check-sat)
(get-model)
