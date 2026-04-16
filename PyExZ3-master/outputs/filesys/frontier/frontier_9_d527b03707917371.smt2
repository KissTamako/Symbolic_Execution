(set-logic ALL)
; Frontier Constraint ID: d527b03707917371
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2449)) (False)
(assert (not (= x 2449)))

; Query: ((== x 2450)) (False)
(assert (not (not (= x 2450))))

(check-sat)
(get-model)
