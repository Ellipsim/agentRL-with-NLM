

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b5)
(on-table b2)
(on b3 b2)
(on b4 b1)
(on b5 b3)
(on b6 b9)
(on b7 b6)
(on-table b8)
(on-table b9)
(on b10 b11)
(on b11 b8)
(clear b4)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b7)
(on b3 b11)
(on b4 b6)
(on b5 b10)
(on b6 b8)
(on b7 b5)
(on b8 b9)
(on b9 b2)
(on b10 b3))
)
)


