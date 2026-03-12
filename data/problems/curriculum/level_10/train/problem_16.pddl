

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on-table b1)
(on b2 b8)
(on-table b3)
(on b4 b10)
(on b5 b2)
(on b6 b4)
(on b7 b6)
(on b8 b7)
(on b9 b5)
(on b10 b1)
(on b11 b3)
(clear b9)
(clear b11)
)
(:goal
(and
(on b2 b4)
(on b3 b7)
(on b4 b9)
(on b6 b10)
(on b7 b11)
(on b8 b5)
(on b9 b6)
(on b11 b1))
)
)


