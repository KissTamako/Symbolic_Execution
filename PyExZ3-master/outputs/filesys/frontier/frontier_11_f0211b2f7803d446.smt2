(set-logic ALL)
; Frontier Constraint ID: f0211b2f7803d446
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2452)) (False)
(assert (not (= x 2452)))

; Query: ((== x 2453)) (False)
(assert (not (not (= x 2453))))

(check-sat)
(get-model)
