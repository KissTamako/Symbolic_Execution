(set-logic ALL)
; Constraint ID: 01ddb13150d27393
; Generated at: 2026-04-16 11:54:14
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60586)) (False)
(assert (not (= x 60586)))

; Query: ((== x 60587)) (False)
(assert (not (not (= x 60587))))

(check-sat)
(get-model)
