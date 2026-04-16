(set-logic ALL)
; Frontier Constraint ID: a10ef1cfb10b6eee
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2437)) (False)
(assert (not (= x 2437)))

; Query: ((== x 2438)) (False)
(assert (not (not (= x 2438))))

(check-sat)
(get-model)
