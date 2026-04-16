(set-logic ALL)
; Frontier Constraint ID: 07e91d109eac9989
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1492)) (False)
(assert (not (= x 1492)))

; Query: ((== x 1493)) (False)
(assert (not (not (= x 1493))))

(check-sat)
(get-model)
