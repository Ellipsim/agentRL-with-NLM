

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b8)
(on b2 b6)
(on-table b3)
(on b4 b10)
(on b5 b2)
(on b6 b1)
(on b7 b5)
(on b8 b9)
(on b9 b4)
(on-table b10)
(on b11 b3)
(clear b7)
(clear b11)
)
(:goal
(and
(on b2 b7)
(on b3 b5)
(on b5 b6)
(on b6 b11)
(on b7 b8)
(on b10 b1))
)
)


