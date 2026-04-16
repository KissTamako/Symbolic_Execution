(set-logic ALL)
; Frontier Constraint ID: 2cbc0df2d6bc5b3b
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1027)) (False)
(assert (not (= x 1027)))

; Query: ((== x 1028)) (False)
(assert (not (not (= x 1028))))

(check-sat)
(get-model)
