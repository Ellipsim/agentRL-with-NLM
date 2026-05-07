

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b7)
(on b3 b9)
(ontable b4)
(on b5 b6)
(on b6 b2)
(on b7 b3)
(on b8 b10)
(on b9 b8)
(ontable b10)
(ontable b11)
(clear b1)
(clear b5)
(clear b11)
)
(:goal
(and
(on b1 b6)
(on b3 b8)
(on b4 b7)
(on b5 b11)
(on b7 b1)
(on b8 b4)
(on b9 b10)
(on b10 b3)
(on b11 b2))
)
)


