

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b11)
(ontable b2)
(on b3 b9)
(on b4 b7)
(on b5 b3)
(on b6 b4)
(on b7 b5)
(ontable b8)
(on b9 b2)
(on b10 b8)
(on b11 b6)
(clear b1)
(clear b10)
)
(:goal
(and
(on b1 b3)
(on b2 b5)
(on b3 b4)
(on b4 b8)
(on b8 b9)
(on b9 b11)
(on b10 b6))
)
)


