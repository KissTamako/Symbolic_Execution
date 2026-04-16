(set-logic ALL)
; Frontier Constraint ID: 832a430fefb9b06a
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 739)) (False)
(assert (not (= x 739)))

; Query: ((== x 740)) (False)
(assert (not (not (= x 740))))

(check-sat)
(get-model)
