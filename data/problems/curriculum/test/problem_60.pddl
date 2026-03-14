

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b11)
(on b2 b5)
(on-table b3)
(on b4 b9)
(on b5 b3)
(on b6 b10)
(on-table b7)
(on b8 b7)
(on-table b9)
(on-table b10)
(on b11 b2)
(clear b1)
(clear b4)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b10)
(on b3 b2)
(on b4 b7)
(on b5 b8)
(on b6 b4)
(on b7 b11)
(on b8 b9)
(on b10 b3)
(on b11 b1))
)
)


