

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(on b3 b4)
(on b4 b7)
(on b5 b6)
(on b6 b11)
(on b7 b5)
(on b8 b2)
(on b9 b3)
(ontable b10)
(ontable b11)
(clear b1)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b10)
(on b3 b2)
(on b7 b5)
(on b8 b11)
(on b10 b3)
(on b11 b7))
)
)


