

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on b3 b11)
(on b4 b13)
(on b5 b9)
(on b6 b8)
(on-table b7)
(on b8 b12)
(on b9 b3)
(on b10 b2)
(on b11 b7)
(on b12 b10)
(on-table b13)
(clear b1)
(clear b5)
(clear b6)
)
(:goal
(and
(on b2 b9)
(on b3 b6)
(on b4 b11)
(on b6 b13)
(on b7 b5)
(on b8 b3)
(on b10 b7)
(on b11 b10)
(on b13 b4))
)
)


