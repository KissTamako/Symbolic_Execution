(set-logic ALL)
; Frontier Constraint ID: 8b196b07f852d088
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1849)) (False)
(assert (not (= x 1849)))

; Query: ((== x 1850)) (False)
(assert (not (not (= x 1850))))

(check-sat)
(get-model)
