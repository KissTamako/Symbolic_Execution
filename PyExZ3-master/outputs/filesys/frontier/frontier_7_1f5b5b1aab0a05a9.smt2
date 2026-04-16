(set-logic ALL)
; Frontier Constraint ID: 1f5b5b1aab0a05a9
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2446)) (False)
(assert (not (= x 2446)))

; Query: ((== x 2447)) (False)
(assert (not (not (= x 2447))))

(check-sat)
(get-model)
