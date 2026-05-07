

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b11)
(on b3 b5)
(on b4 b6)
(ontable b5)
(on b6 b9)
(on b7 b4)
(on b8 b7)
(ontable b9)
(ontable b10)
(on b11 b1)
(clear b2)
(clear b3)
(clear b8)
(clear b10)
)
(:goal
(and
(on b1 b11)
(on b3 b8)
(on b4 b10)
(on b5 b4)
(on b6 b2)
(on b7 b6)
(on b9 b5))
)
)


