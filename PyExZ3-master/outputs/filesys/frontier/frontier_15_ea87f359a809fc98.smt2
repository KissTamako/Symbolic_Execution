(set-logic ALL)
; Frontier Constraint ID: ea87f359a809fc98
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2458)) (False)
(assert (not (= x 2458)))

; Query: ((== x 2459)) (False)
(assert (not (not (= x 2459))))

(check-sat)
(get-model)
