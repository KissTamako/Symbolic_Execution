(set-logic ALL)
; Executed Path ID: 736bf9ddc142f9b8
; Generated at: 2026-04-17 03:12:42
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const i Int)

; ((== i 1)) (False)
(assert (not (= i 1)))
; ((== i 4)) (False)
(assert (not (= i 4)))
; ((== i 6)) (True)
(assert (= i 6))

(check-sat)
(get-model)
