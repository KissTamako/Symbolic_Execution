(set-logic ALL)
; Frontier Constraint ID: 4edb621c717aaba9
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 523)) (False)
(assert (not (= x 523)))

; Query: ((== x 524)) (False)
(assert (not (not (= x 524))))

(check-sat)
(get-model)
