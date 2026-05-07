

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(on b3 b5)
(on b4 b1)
(on b5 b11)
(ontable b6)
(on b7 b4)
(ontable b8)
(on b9 b6)
(ontable b10)
(ontable b11)
(clear b2)
(clear b3)
(clear b7)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b11)
(on b3 b10)
(on b4 b3)
(on b7 b4)
(on b8 b5)
(on b9 b8)
(on b10 b6)
(on b11 b9))
)
)


