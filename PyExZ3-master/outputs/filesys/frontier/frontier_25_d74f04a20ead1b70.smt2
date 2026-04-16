(set-logic ALL)
; Frontier Constraint ID: d74f04a20ead1b70
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 748)) (False)
(assert (not (= x 748)))

; Query: ((== x 749)) (False)
(assert (not (not (= x 749))))

(check-sat)
(get-model)
