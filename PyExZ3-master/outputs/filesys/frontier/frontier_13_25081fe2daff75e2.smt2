(set-logic ALL)
; Frontier Constraint ID: 25081fe2daff75e2
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1855)) (False)
(assert (not (= x 1855)))

; Query: ((== x 1856)) (False)
(assert (not (not (= x 1856))))

(check-sat)
(get-model)
