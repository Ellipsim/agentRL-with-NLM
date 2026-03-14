

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on-table b1)
(on b2 b9)
(on-table b3)
(on b4 b5)
(on-table b5)
(on b6 b13)
(on b7 b10)
(on b8 b12)
(on b9 b6)
(on b10 b4)
(on b11 b2)
(on b12 b7)
(on b13 b1)
(clear b3)
(clear b8)
(clear b11)
)
(:goal
(and
(on b1 b2)
(on b4 b1)
(on b5 b8)
(on b6 b10)
(on b8 b7)
(on b9 b11)
(on b10 b4)
(on b12 b5)
(on b13 b3))
)
)


